import nox

@nox.session(python=["3.10", "3.9"])
def tests(session):
    session.run("poetry", "install", external=True)
    session.run("pytest", *session.posargs)