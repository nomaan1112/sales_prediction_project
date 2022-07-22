from sales.pipeline.pipeline import Pipeline
from sales.logger import logging
from sales.exception import SalesException

def main():
    try:
        pipeline= Pipeline()
        pipeline.run_pipeline()

    except Exception as e:
        logging.error(f"{e}")
        print(e)  

if __name__== "__main__":
    main()

