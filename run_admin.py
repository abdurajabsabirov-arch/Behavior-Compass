"""Admin панель на FastAPI"""

import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.database import init_db, get_session, async_session_maker
from app.db.models import User, Result, Feedback, Referral
from app.services.excel_export import ExcelExportService

# Загружаем переменные окружения
load_dotenv()

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем приложение
app = FastAPI(title="Behavior Compass Admin")

# Настраиваем шаблоны
templates_dir = os.path.join(os.path.dirname(__file__), "app", "admin", "templates")
if os.path.exists(templates_dir):
    templates = Jinja2Templates(directory=templates_dir)


# Middleware для инициализации БД
@app.on_event("startup")
async def startup():
    """Инициализация БД при запуске"""
    await init_db()
    logger.info("✅ Admin panel started")


# Главная страница
@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Главная страница админ-панели"""
    
    async with async_session_maker() as session:
        # Получаем статистику
        users_stmt = select(User)
        users_result = await session.execute(users_stmt)
        total_users = len(users_result.scalars().all())
        
        results_stmt = select(Result).where(Result.completed == True)
        results_result = await session.execute(results_stmt)
        total_results = len(results_result.scalars().all())
        
        feedback_stmt = select(Feedback)
        feedback_result = await session.execute(feedback_stmt)
        total_feedback = len(feedback_result.scalars().all())
        
        referrals_stmt = select(Referral)
        referrals_result = await session.execute(referrals_stmt)
        total_referrals = len(referrals_result.scalars().all())
    
    # Генерируем простой HTML
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Behavior Compass Admin</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            h1 {{ color: #333; }}
            .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 20px 0; }}
            .stat-card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .stat-card h2 {{ margin: 0; color: #4472C4; }}
            .stat-card .value {{ font-size: 32px; font-weight: bold; color: #333; }}
            .nav {{ background: white; padding: 15px; border-radius: 8px; margin-bottom: 20px; }}
            .nav a {{ margin-right: 15px; text-decoration: none; color: #4472C4; }}
            .nav a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎯 Behavior Compass - Admin Dashboard</h1>
            
            <div class="nav">
                <a href="/users">👥 Users</a>
                <a href="/results">📊 Results</a>
                <a href="/feedback">💬 Feedback</a>
                <a href="/referrals">🔗 Referrals</a>
                <a href="/export">📥 Export</a>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <h2>Total Users</h2>
                    <div class="value">{total_users}</div>
                </div>
                <div class="stat-card">
                    <h2>Completed Tests</h2>
                    <div class="value">{total_results}</div>
                </div>
                <div class="stat-card">
                    <h2>Feedback Received</h2>
                    <div class="value">{total_feedback}</div>
                </div>
                <div class="stat-card">
                    <h2>Referrals</h2>
                    <div class="value">{total_referrals}</div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content


# API для пользователей
@app.get("/users")
async def get_users_page():
    """Страница пользователей"""
    
    async with async_session_maker() as session:
        stmt = select(User)
        result = await session.execute(stmt)
        users = result.scalars().all()
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Users</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
            th { background-color: #4472C4; color: white; }
            tr:nth-child(even) { background-color: #f2f2f2; }
            a { color: #4472C4; text-decoration: none; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <h1>👥 Users</h1>
        <a href="/">← Back to Dashboard</a>
        <table>
            <tr>
                <th>ID</th>
                <th>Telegram ID</th>
                <th>Username</th>
                <th>Phone</th>
                <th>Language</th>
                <th>Created At</th>
            </tr>
    """
    
    for user in users:
        html_content += f"""
            <tr>
                <td>{user.id}</td>
                <td>{user.telegram_id}</td>
                <td>{user.username}</td>
                <td>{user.phone}</td>
                <td>{user.language}</td>
                <td>{user.created_at.strftime("%Y-%m-%d %H:%M")}</td>
            </tr>
        """
    
    html_content += """
        </table>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)


# API для результатов
@app.get("/results")
async def get_results_page():
    """Страница результатов"""
    
    async with async_session_maker() as session:
        stmt = select(Result)
        result = await session.execute(stmt)
        results = result.scalars().all()
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Results</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            table { border-collapse: collapse; width: 100%; font-size: 12px; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #4472C4; color: white; }
            tr:nth-child(even) { background-color: #f2f2f2; }
            a { color: #4472C4; text-decoration: none; }
        </style>
    </head>
    <body>
        <h1>📊 Test Results</h1>
        <a href="/">← Back to Dashboard</a>
        <table>
            <tr>
                <th>ID</th>
                <th>Telegram ID</th>
                <th>Blue</th>
                <th>Green</th>
                <th>Yellow</th>
                <th>Red</th>
                <th>Primary</th>
                <th>Secondary</th>
                <th>Completed</th>
                <th>Created At</th>
            </tr>
    """
    
    for res in results:
        html_content += f"""
            <tr>
                <td>{res.id}</td>
                <td>{res.telegram_id}</td>
                <td>{res.blue_score}</td>
                <td>{res.green_score}</td>
                <td>{res.yellow_score}</td>
                <td>{res.red_score}</td>
                <td>{res.primary_color}</td>
                <td>{res.secondary_color}</td>
                <td>{'✅' if res.completed else '❌'}</td>
                <td>{res.created_at.strftime("%Y-%m-%d %H:%M")}</td>
            </tr>
        """
    
    html_content += """
        </table>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)


# API для отзывов
@app.get("/feedback")
async def get_feedback_page():
    """Страница отзывов"""
    
    async with async_session_maker() as session:
        stmt = select(Feedback)
        result = await session.execute(stmt)
        feedbacks = result.scalars().all()
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Feedback</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            table { border-collapse: collapse; width: 100%; font-size: 12px; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #4472C4; color: white; }
            tr:nth-child(even) { background-color: #f2f2f2; }
            a { color: #4472C4; text-decoration: none; }
        </style>
    </head>
    <body>
        <h1>💬 Feedback</h1>
        <a href="/">← Back to Dashboard</a>
        <table>
            <tr>
                <th>ID</th>
                <th>Telegram ID</th>
                <th>Rating</th>
                <th>Comment</th>
                <th>Agree Referral</th>
                <th>Created At</th>
            </tr>
    """
    
    for fb in feedbacks:
        html_content += f"""
            <tr>
                <td>{fb.id}</td>
                <td>{fb.telegram_id}</td>
                <td>{'⭐' * fb.rating}</td>
                <td>{fb.comment or '-'}</td>
                <td>{'✅' if fb.agree_referral else '❌'}</td>
                <td>{fb.created_at.strftime("%Y-%m-%d %H:%M")}</td>
            </tr>
        """
    
    html_content += """
        </table>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)


# API для рефералов
@app.get("/referrals")
async def get_referrals_page():
    """Страница рефералов"""
    
    async with async_session_maker() as session:
        stmt = select(Referral)
        result = await session.execute(stmt)
        referrals = result.scalars().all()
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Referrals</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
            th { background-color: #4472C4; color: white; }
            tr:nth-child(even) { background-color: #f2f2f2; }
            a { color: #4472C4; text-decoration: none; }
        </style>
    </head>
    <body>
        <h1>🔗 Referrals</h1>
        <a href="/">← Back to Dashboard</a>
        <table>
            <tr>
                <th>ID</th>
                <th>Referrer ID</th>
                <th>Referred ID</th>
                <th>Completed Test</th>
                <th>Created At</th>
            </tr>
    """
    
    for ref in referrals:
        html_content += f"""
            <tr>
                <td>{ref.id}</td>
                <td>{ref.referrer_id}</td>
                <td>{ref.referred_id}</td>
                <td>{'✅' if ref.completed_test else '❌'}</td>
                <td>{ref.created_at.strftime("%Y-%m-%d %H:%M")}</td>
            </tr>
        """
    
    html_content += """
        </table>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)


# API для экспорта
@app.get("/export")
async def export_page():
    """Страница экспорта"""
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Export Data</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; }
            h1 { color: #333; }
            .export-btn { display: inline-block; margin: 10px 10px 10px 0; padding: 10px 20px; background-color: #4472C4; color: white; text-decoration: none; border-radius: 4px; }
            .export-btn:hover { background-color: #2d5a9e; }
            a { color: #4472C4; text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📥 Export Data</h1>
            <a href="/">← Back to Dashboard</a>
            
            <h2>Download Excel Files</h2>
            <a href="/export/users" class="export-btn">📋 Export Users</a>
            <a href="/export/results" class="export-btn">📊 Export Results</a>
            <a href="/export/feedback" class="export-btn">💬 Export Feedback</a>
            <a href="/export/referrals" class="export-btn">🔗 Export Referrals</a>
        </div>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)


# Endpoints для скачивания файлов
@app.get("/export/users")
async def export_users():
    """Экспорт пользователей в Excel"""
    
    async with async_session_maker() as session:
        output_path = await ExcelExportService.export_users(session)
    
    return FileResponse(output_path, filename="users.xlsx")


@app.get("/export/results")
async def export_results():
    """Экспорт результатов в Excel"""
    
    async with async_session_maker() as session:
        output_path = await ExcelExportService.export_results(session)
    
    return FileResponse(output_path, filename="results.xlsx")


@app.get("/export/feedback")
async def export_feedback():
    """Экспорт отзывов в Excel"""
    
    async with async_session_maker() as session:
        output_path = await ExcelExportService.export_feedback(session)
    
    return FileResponse(output_path, filename="feedback.xlsx")


@app.get("/export/referrals")
async def export_referrals():
    """Экспорт рефералов в Excel"""
    
    async with async_session_maker() as session:
        output_path = await ExcelExportService.export_referrals(session)
    
    return FileResponse(output_path, filename="referrals.xlsx")


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("ADMIN_PORT", 8000))
    logger.info(f"Starting admin panel on http://127.0.0.1:{port}")
    
    uvicorn.run(app, host="127.0.0.1", port=port)
