FROM python:3.10-slim

WORKDIR /app

# Upgrade pip to the latest version
RUN pip install --upgrade pip

RUN pip install babel
RUN pip install pandas_ta
RUN pip install scikit-learn
RUN pip install flask==2.2.5
RUN pip install flask-cors==5.0.0
RUN pip install apscheduler==3.10.4
RUN pip install requests==2.31.0
RUN pip install beautifulsoup4==4.12.3
RUN pip install lxml==5.3.0
RUN pip install transformers==4.30.2
RUN pip install tensorflow==2.12.0
RUN pip install pandas==1.5.3
RUN pip install numpy==1.23.5 --only-binary=:all:

# Copy the rest of the application
COPY . /app

# Expose the application port
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
