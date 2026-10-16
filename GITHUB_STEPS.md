# Реальные действия GitHub для лабораторных №7–8

Нужен собственный GitHub-репозиторий `library-project` (его URL будет зависеть от аккаунта).

```bash
git init
git add .
git commit -m "Initial library project"
git branch -M main
git remote add origin https://github.com/USERNAME/library-project.git
git push -u origin main

git switch -c feature/add-reader
# Внесите отдельное изменение в database.py (например, уточните docstring add_reader).
git add database.py
git commit -m "Document add_reader function"
git push -u origin feature/add-reader
```

В GitHub откройте **Compare & pull request**, создайте PR из `feature/add-reader` в `main`, затем выполните **Merge pull request**. Сделайте реальные скриншоты ветки, PR и merge. Для демонстрации конфликта создайте две ветки с несовместимыми изменениями одной строки README, объедините одну с main и попытайтесь объединить вторую, затем разрешите конфликт вручную. Не утверждайте, что конфликт/PR выполнены, пока они реально не выполнены.
