from instagrapi import Client


def publish_video(filename=str, ):
    cl = Client()
    cl.login("reddit.daily.vids", "5K#ie,e:V\"a->)p")

    cl.clip_upload(
        filename,
        "",
    )