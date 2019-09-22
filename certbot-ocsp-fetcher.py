import click
import os
import pathlib
import subprocess

@click.command()
@click.option(
    "-n",
    "--cert-name"
    )
@click.option(
    "-c",
    "--certbot-dir",
    default=pathlib.Path("/etc/letsencrypt"),
    type=pathlib.Path,
    help="The configuration directory path of Certbot"
    )
@click.option(
    "-o",
    "--output-dir",
    type=pathlib.Path,
    help="The directory to store OCSP responses in and inspect them from"
    )
@click.option(
    "-v",
    "--verbose/--no-verbose",
    default=False
    )
def main(
        cert_name: str,
        certbot_dir: pathlib.Path,
        output_dir: pathlib.Path,
        verbose: bool) -> None:
    prepare_output_dir(output_dir)
    start_in_correct_mode()

def prepare_output_dir(output_dir: pathlib.Path) -> pathlib.Path:
    if output_dir:
        # To do: Catch exception when output_dir is not writable, and check if
        # that is also triggered when the output_dir already exists
        pathlib.mkdir(output_dir, parents=True, exist_ok=True)
    else:
        return pathlib.Path(".")

def start_in_correct_mode():
    pass

def exit_on_error():
    pass

def run_standalone():
    pass

def run_as_deploy_hook():
    pass

def check_for_existing_ocsp_response():
    pass

def fetch_ocsp_response():
    pass

def print_and_handle_result():
    pass

if __name__ == '__main__':
    main()
