FROM lama-cleaner/lama-cleaner:latest

EXPOSE 8080

CMD ["lama-cleaner", "--model", "lama", "--port", "8080", "--host", "0.0.0.0"]
