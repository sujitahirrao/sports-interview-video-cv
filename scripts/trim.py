
# from moviepy.editor import VideoFileClip

# clip = VideoFileClip(r"https://showcase-raw.s3.amazonaws.com/BHS%20Baseball%20/BHS%20Baseball%20and%20Ramblers/STREAM/00004.MTS?AWSAccessKeyId=ASIAVXRFOTAJR3IPJYHQ&Signature=ynlyJZV6Gv9r7iG%2F0hnyy32w%2Bco%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEL7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCIDhv2%2FFrHLcAgDTBxqJSBJ5qXj%2Fm%2BQottMUX8ELeXC5qAiEA5h9JaArz4A19RUJkdkpGRVhzDk85dRez5O%2FPpGlxwqMqvQIIpv%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgwzOTQxNDE4MDA0NjciDCf7eO45sL7JJvi99CqRAqA9gCFXZ6P0ePw4%2BPIA%2FcolqQeL4Oh1Xxv3kb20FJF2NHwd1FsibFdfk5ZUkfkc4Ov1RzY25PvHbJPd9isRDyAU0z2viBphhvUQFlX1yUK8EKWMVH%2Fy5EFMBE2f7JbIhRxr8SOSiVJIO6I4u2st0wu0pwgdf%2FLuz9BkA0mfB7C%2FnvB8Ub7WN2CYbbhdl40nPa9x9RyA2gOX%2FrS6oGtPNPROY3ogsKIjdCoNyyrx8BnNw4mRxjFAQwzUZcsGSJ7EqGq92M86SP5kcNepvFKMsNTPTK5jUNta2vUAjaYp1q75PxhxRWxEnMPOXLaMoiE2szZv5UAwiTChSm7e653eiNljESPslYyrUaM8jF0sAWmd0jDwttWhBjqTAQGRT4%2FSu0pqqf%2BR%2Fk3Z%2BfZR20dNc0yKO%2FK9%2BS7bihJLAstXVUZD2UEKeL%2F8YDx%2FGAGn4ONcWD8WDBgsbiUQP3EDKlxN7qy%2FOwdgj%2B%2BfFRG7DET9vAIorUckLEMrWau5QzidQiSpuJaSooW9Zq3UdvGjABepQNQ0vaFQRlPkAkRHZz%2B4pc8L1jAvcLaFj7r8d7%2Fvdg%3D%3D&Expires=1681222788")
# clip = clip.subclip(30, 90)

# clip.write_videofile(f"{f['Key'].split('/')[-1]}.mp4")


import ffmpeg


def trim(in_file, out_file, start, end):
    # if os.path.exists(out_file):
    #     os.remove(out_file)

    # in_file_probe_result = ffmpeg.probe(in_file)
    # in_file_duration = in_file_probe_result.get(
    #     "format", {}).get("duration", None)
    # print(in_file_duration)

    input_stream = ffmpeg.input(in_file)

    pts = "PTS-STARTPTS"
    video = input_stream.trim(start=start, end=end).setpts(pts)
    audio = (input_stream
             .filter_("atrim", start=start, end=end)
             .filter_("asetpts", pts))
    video_and_audio = ffmpeg.concat(video, audio, v=1, a=1)
    output = ffmpeg.output(video_and_audio, out_file, format="mp4")
    output.run()

    # out_file_probe_result = ffmpeg.probe(out_file)
    # out_file_duration = out_file_probe_result.get(
    #     "format", {}).get("duration", None)
    # print(out_file_duration)


trim(r"/mnt/d/Machine Vision/Sports Video CV/interview-detection/data/interim/BHS Baseball/00017.MTS", 
     "out-00017.mp4", 0, 70)
