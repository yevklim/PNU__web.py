# Лабораторна робота №10

## Модулі (blueprints)

### Модуль `base`

Використовує URL-префікс `/base`.

Містить статичні файли (Bootstrap, кастомні JS і CSS) і базові Jinja2-темплейти - base.html, base_nav.html, macros.html.

Також містить підмодуль `menu`, який створює і дозволяє конфігурувати навігаційне меню для сайту.

### Модуль `user`

Використовує URL-префікс `/user`.

Надає доступ до сторінок та функціоналу для реєстрації, авторизації, профілю користувача та списку користувачів.

Містить модель `User` і WTF-форми.

У статичній папці зберігає зображення профілів користувачів.

### Модуль `todo`

Використовує URL-префікс `/todo`.

Надає доступ до сторінок та функціоналу to-do.

Містить модель `ToDo` і WTF-форму `ToDoForm`.

### Модуль `feedback`

Використовує URL-префікс `/feedback`.

Надає доступ до сторінок та функціоналу для відправки і перегляду відгуків.

Містить модель `FeedBack` і WTF-форму `FeedBackForm`.

### Модуль `cookies`

Використовує URL-префікс `/cookies`.

Надає доступ до сторінок та функціоналу для роботи з кукі.

### Модуль `portfolio`

Використовує URL-префікс `/portfolio`.

Надає доступ до сторінок псевдо-портфоліо.

## Вигляд сайту для авторизованого користувача зі сторінки `/user/account`
![](./screenshots/Page%20Account.png)

## Вигляд сайту для неавторизованого користувача зі сторінки `/user/login`
![](./screenshots/Page%20Sign%20In.png)
