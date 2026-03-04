# -- coding: utf-8 --
# -必备模块
import main_yinru
import public
# --------------

def main():
    main_yinru.main()


if __name__ == '__main__':
    try:
        main()
    except:
        public.try_error('主入口')
