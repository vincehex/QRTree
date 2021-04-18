import os
import time

import django

from Display.models import User

# 在environ字典里设置默认Django环境，'xxxx.settings'指Django项目的配置文件
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'QRTree.settings')
django.setup()

User.objects.create_superuser(username='admin', password='admin', email='admin@admin.com',
                              birthdate=time.strftime("%Y-%m-%d")
                              , sex='male', phone='13283829947', IDCard='213213213213')
