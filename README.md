### Використання образу з Dockerhub

```bash
docker pull timofey282228/nta-lab1:latest
docker tag timofey282228/nta-lab1:nta_lab1 nta_lab1  #  для зручності у подальших прикладах
```

### Збірка образу

```bash
git clone https://github.com/timofey282228/nta-lab1.git
cd nta_lab1
docker build -t ntalab1 .
```

### Тестування

**1. Факторизація числа (n):**

```bash
docker run --rm ntalab1 123456
```

**2. Використання методу Полларда з модифікацією:**

```bash
docker run --rm ntalab1 123456 --pollard_mod floyd
```

**3. Виведення у форматі LaTeX:**

```bash
docker run --rm ntalab1 123456 --latex
```

**4. Запуск із параметрами для методу Бріллхарта-Моррісона:**

```bash
docker run --rm ntalab1 123456 -k 7 --attempts 5
```

**5. вказівка кількості раундів тесту простоти:**

```bash
docker run --rm ntalab1 123456 -m 10
```

**6. Запуск у режимі порівняння швидкості факторизації:**

```bash
docker run --rm ntalab1 --algospeed 123456 654321
```

### Загальні поради щодо використання:

- Прапор `--rm` видаляє контейнер після його зупинки, що допомагає зберегти вашу систему чистою від невикористовуваних контейнерів.

