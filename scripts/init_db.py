#!/usr/bin/env python3
# ===========================================
# AI Code Quality Assistant - 数据库初始化脚本
# ===========================================

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.core.database import Base, engine
from backend.models.user import User
from backend.models.project import Project
from backend.models.analysis import AnalysisResult

def create_tables():
    """创建数据库表"""
    print("🔧 创建数据库表...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ 数据库表创建成功")
    except Exception as e:
        print(f"❌ 创建表失败: {e}")
        return False
    return True

def init_basic_data():
    """初始化基础数据"""
    print("📊 初始化基础数据...")
    try:
        from sqlalchemy.orm import sessionmaker
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # 创建默认管理员用户
        admin_user = User(
            username="admin",
            email="admin@aicodequality.dev",
            full_name="系统管理员",
            is_active=True,
            is_superuser=True
        )
        admin_user.set_password("admin123")
        
        # 检查是否已存在
        existing_admin = db.query(User).filter(User.username == "admin").first()
        if not existing_admin:
            db.add(admin_user)
            print("✅ 创建默认管理员用户: admin/admin123")
        
        db.commit()
        db.close()
        print("✅ 基础数据初始化成功")
        return True
        
    except Exception as e:
        print(f"❌ 初始化数据失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始初始化 AI Code Quality Assistant 数据库...")
    
    # 创建表
    if not create_tables():
        sys.exit(1)
    
    # 初始化数据
    if not init_basic_data():
        sys.exit(1)
    
    print("🎉 数据库初始化完成！")
    print("\n📝 默认登录信息:")
    print("   用户名: admin")
    print("   密码: admin123")
    print("\n⚠️  请在生产环境中立即修改默认密码！")

if __name__ == "__main__":
    main()