def pytest_addoption(parser):
    parser.addoption(
        "--url",
        action="store",
        default="https://ya.ru",
        help="This is request url"
    )

    parser.addoption(
        "--encoding",
        action="store",
        default="UTF-8",
        help="This is request url"
    )