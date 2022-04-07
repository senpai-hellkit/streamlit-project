from invoke import task


@task
def start(c):
    c.run("streamlit run main.py")
