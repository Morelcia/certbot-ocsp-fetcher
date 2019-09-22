import click
import os
import pathlib
import psutil
import subprocess
import tempfile

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
    start_in_correct_mode(verbose)

def prepare_output_dir(output_dir: pathlib.Path) -> pathlib.Path:
    if output_dir:
        # To do: Catch exception when output_dir is not writable, and check if
        # that is also triggered when the output_dir already exists
        pathlib.mkdir(output_dir, parents=True, exist_ok=True)
    else:
        return pathlib.Path(".")

def start_in_correct_mode(verbose: bool) -> None:
    temp_output_dir: pathlib.Path = tempfile.TemporaryDirectory()

    responses_fetched: int

    # These two environment variables are set if this script is invoked by
    # Certbot
    if "RENEWED_DOMAINS" in os.environ and "RENEWED_LINEAGE" in os.environ:
        responses_fetched = run_as_deploy_hook(temp_output_dir)
    else:
        responses_fetched = run_standalone(temp_output_dir=temp_output_dir)

    if responses_fetched > 0:
        print_and_handle_result(responses_fetched=responses_fetched, verbose=verbose)

def exit_on_error():
    pass

def run_standalone(temp_output_dir: pathlib.Path):
    return 0

def run_as_deploy_hook():
    return 0

def check_for_existing_ocsp_response():
    pass

def fetch_ocsp_response():
    pass

def print_and_handle_result(responses_fetched: int, verbose: bool) -> None:
    manage_nginx: bool = False
    for process in psutil.process_iter():
        try:
            process_info = process.as_dict(attrs=['pid', 'name', 'uids'])
            if process_info.name == "nginx" and process_info.uids(effective) == os.getuid():
                manage_nginx = True
                break
        except psutil.NoSuchProcess:
            pass
    if manage_nginx:
        # To do: Send SIGHUP to nginx
        if verbose:
            click.echo("nginx:\t\treloaded", err=True)
            pass
    elif verbose:
        click.echo("nginx:\t\tnot reloaded\tunprivileged, reload manually", err=True)

if __name__ == '__main__':
    main()
