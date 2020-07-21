import os

from invoke.tasks import task

PROJECT_NAME = os.environ["PROJECT_NAME"]


@task
def install_js(c):
    with c.cd("/project"):
        print("\nInstall Javascript dependencies\n")
        c.run("source /root/.nvm/nvm.sh && nvm install --lts", pty=True)
        c.run("npm install")


@task
def install_python(c):
    with c.cd("/project"):
        print("\nInstall Python dependencies\n")
        c.run("poetry install")


@task(pre=[install_js, install_python])
def setup(c):
    print("Project setup complete.")


@task
def lint(c):
    c.run("poetry run pre-commit run --all-files", pty=True)


@task
def requirements(c, export_path=f"{PROJECT_NAME}/requirements.txt"):
    print(f"Exporting app requirements.txt: {export_path}")
    with c.cd(f"/project"):
        c.run(f"poetry export -f requirements.txt --without-hashes -o {export_path}")


@task
def css(c):
    with c.cd("/project"):
        c.run(f"npm run css", pty=True)


@task(pre=[requirements, css])
def deploy(c):
    with c.cd(f"/project/{PROJECT_NAME}"):
        c.run("poetry run chalice deploy", pty=True)


@task
def teardown(c):
    with c.cd(f"/project/{PROJECT_NAME}"):
        c.run("poetry run chalice delete", pty=True)


@task
def py_shell(c):
    c.run("poetry run ipython", pty=True)


@task
def serve(c):
    c.run("python3 -m http.server 8000 --bind 127.0.0.1")
