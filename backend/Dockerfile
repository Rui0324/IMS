FROM python:3.12-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 1) apt 依赖（mysqlclient 编译必需）
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    default-libmysqlclient-dev \
  && rm -rf /var/lib/apt/lists/*

# 2) pip 改国内源 + 超时重试（解决 pythonhosted 超时）
RUN mkdir -p /etc/pip && cat > /etc/pip.conf <<'PIP'
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
trusted-host = pypi.tuna.tsinghua.edu.cn
timeout = 120
retries = 10
PIP

COPY requirements.txt /app/requirements.txt

# 3) 安装依赖
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
