from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import uvicorn

app = FastAPI(title='Result TestAPI', version='1.0.0')

# Модели Pydantic
class TestResultItem(BaseModel):
    id: int
    user_name: str
    test_name: str
    total_questions: int
    correct_answers: int
    percent_correct_answers: float
    time_complete: int
    user_id: int


class TestResult(BaseModel):
    user_name: str
    test_name: str
    total_questions: int
    correct_answers: int
    percent_correct_answers: float
    time_complete: int
    user_answers: Optional[List[int]] = None


class TestResultResponse(BaseModel):
    status: str
    message: str
    result_id: Optional[int] = None
    user_id: Optional[int] = None


class TestResultsShow(BaseModel):
    status: str
    message: str
    results: List[TestResultItem]


class DeleteRequest(BaseModel):
    ids: List[int]


class DeleteResponse(BaseModel):
    status: str
    message: str
    deleted_count: int


def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname='ShumovVDBForTestApp',
            user='postgres',
            password='1234',
            host='localhost',
            port='5433'
        )
        return conn
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f'Database connection error: {str(e)}')


@app.post("/api/save_test_result", response_model=TestResultResponse)
async def save_test_result(result_data: TestResult):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Находим или создаём пользователя
        cursor.execute('SELECT id FROM users WHERE name = %s', (result_data.user_name,))
        user_result = cursor.fetchone()

        if user_result:
            user_id = user_result[0]
        else:
            # Создаем нового пользователя
            cursor.execute('INSERT INTO users (name) VALUES (%s) RETURNING id', (result_data.user_name,))
            user_id = cursor.fetchone()[0]

        # Сохраняем результаты теста
        cursor.execute('''INSERT INTO test_info 
                (user_name, test_name, total_questions, correct_answers, percent_correct_answers, time_complete, user_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id''',
                       (result_data.user_name, result_data.test_name, result_data.total_questions,
                        result_data.correct_answers, result_data.percent_correct_answers,
                        result_data.time_complete, user_id))

        result_id = cursor.fetchone()[0]
        conn.commit()

        return TestResultResponse(
            status='success',
            message="Results saved successfully",
            result_id=result_id,
            user_id=user_id
        )

    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    finally:
        if conn:
            conn.close()


@app.get('/api/show_tests_results', response_model=TestResultsShow)
async def show_tests_results():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute('SELECT * FROM test_info ORDER BY id ASC')
        users_data = cursor.fetchall()

        results = []
        for row in users_data:
            results.append(TestResultItem(
                id=row['id'],
                user_name=row['user_name'],
                test_name=row['test_name'],
                total_questions=row['total_questions'],
                correct_answers=row['correct_answers'],
                percent_correct_answers=float(row['percent_correct_answers']),
                time_complete=row['time_complete'],
                user_id=row['user_id']
            ))

        return TestResultsShow(
            status="success",
            message="Results retrieved successfully",
            results=results
        )

    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    finally:
        if conn:
            conn.close()


@app.delete('/api/delete_results', response_model=DeleteResponse)
async def delete_results(delete_request: DeleteRequest):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if not delete_request.ids:
            return DeleteResponse(
                status="error",
                message="No IDs provided",
                deleted_count=0
            )

        # Создаем плейсхолдеры для IN условия
        placeholders = ','.join(['%s'] * len(delete_request.ids))

        # Удаляем записи
        cursor.execute(f'DELETE FROM test_info WHERE id IN ({placeholders})', delete_request.ids)
        deleted_count = cursor.rowcount

        conn.commit()

        return DeleteResponse(
            status="success",
            message=f"Deleted {deleted_count} records",
            deleted_count=deleted_count
        )

    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    finally:
        if conn:
            conn.close()


@app.delete("/api/clear_all_results", response_model=DeleteResponse)
async def clear_all_results():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Удаляем все записи
        cursor.execute('DELETE FROM test_info')
        deleted_count = cursor.rowcount

        cursor.execute('ALTER SEQUENCE test_info_id_seq RESTART WITH 1')

        conn.commit()

        return DeleteResponse(
            status="success",
            message=f"All records deleted ({deleted_count} total)",
            deleted_count=deleted_count
        )

    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
