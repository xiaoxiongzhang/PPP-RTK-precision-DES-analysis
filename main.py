from core import Application

if __name__ == '__main__':
    from config import Content, CONFIG

    c = Content(
        INPUT_PATH=CONFIG.INPUT_PATH,
        COLUMNS=CONFIG.COLUMNS,
        THRESHOLD=CONFIG.THRESHOLD,
        PRECISION=CONFIG.PRECISION,
        PRECISION_MAPPING=CONFIG.PRECISION_MAPPING,
        OUTPUT_PATH=CONFIG.OUTPUT_PATH,
        PLOT=CONFIG.PLOT,
        SHOW_PIC=CONFIG.SHOW_PIC,
        TRUNCATE=CONFIG.TRUNCATE,
        SEP=CONFIG.SEP,
    )
    print(c)

    Application(c).run()
