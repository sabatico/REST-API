#use python v3.11
FROM python:3.11

#open port 5000
EXPOSE 5000

#move into the /app directory
WORKDIR /app

#copy requirements in current docker folder
COPY requirements.txt .

#pip
RUN pip install -r requirements.txt

#copy all from original root (.) into the /app directory where we moved using WORKDIR now (.)
COPY . .

#run the app
CMD ["flask","run", "--host","0.0.0.0"]


