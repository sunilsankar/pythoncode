#!/usr/bin/env python3
#Author Sunil Sankar
#Date 14-April-2026
import argparse
import requests
import subprocess


def git_version(repo):
    r = requests.get(f"https://api.github.com/repos/{repo}/releases/latest")
    r.raise_for_status()
    tag = r.json()["name"]
    tag = tag.strip()
    tag = tag.removeprefix("Version ")
    tag = tag.removeprefix("version ")
    return tag


def docker_version(image, tag):
    token = requests.get(
        "https://auth.docker.io/token",
        params={
            "service": "registry.docker.io",
            "scope": f"repository:{image}:pull",
        },
    ).json()["token"]

    r = requests.get(
        f"https://registry-1.docker.io/v2/{image}/manifests/{tag}",
        headers={
            "Accept": "application/vnd.docker.distribution.manifest.v2+json",
            "Authorization": f"Bearer {token}",
        },
    )
    r.raise_for_status()

    return r.headers["Docker-Content-Digest"]

def send_signal(message):
    url = "http://192.168.1.12:9090/v2/send"
    payload = {
    "message": message,
    "number": "+31686234192",
    "recipients": [
        "group.WU5TT3B3bWVIaCtjbHkvdk8zM2NoOHhid25XOVZXeUdwcEd2MkJzczJFaz0="
    ]}
    r2 = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
    print(r2.status_code, r2.text)

def local_version(image):
    return subprocess.check_output(
        [
            "docker",
            "images",
            "--no-trunc",
            "--format",
            "{{.ID}}",
            image,
        ],
        text=True,
    ).strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("image", help="docker image name (org/image)")
    parser.add_argument(
        "--github",
        help="github repo (org/repo). default = same as image",
    )

    args = parser.parse_args()

    github_repo = args.github or args.image

    tag = git_version(github_repo)
    remote_digest = docker_version(args.image, tag)
    local_digest = local_version(args.image)
    if remote_digest == local_digest:
        output = (
                   f"tag: {tag}\n"
                   f"remote: {remote_digest}\n"
                   f"local: {local_digest}\n"
                   f"{args.image} is up2date"
                 )
        print(output)
    else:
        print(f"{args.image} needs update")
        output = (
                   f"tag: {tag}\n"
                   f"remote: {remote_digest}\n"
                   f"local: {local_digest}\n"
                   f"{args.image} needs update"
                 )
        print(output)
        send_signal(output)


if __name__ == "__main__":
    main()
