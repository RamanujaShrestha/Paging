
def fifo(reference_string, frame_count):
    frames = []
    pointer = 0
    history = []

    for page in reference_string:
        hit = page in frames
        evicted = None

        if not hit:
            if len(frames) < frame_count:
                frames.append(page)
            else:
                evicted = frames[pointer]
                frames[pointer] = page
                pointer = (pointer + 1) % frame_count

        history.append({
            "page": page,
            "frames": frames.copy(),
            "hit": hit,
            "fault": not hit,
            "evicted": evicted
        })

    return history


def lru(reference_string, frame_count):
    frames = []
    last_used = {}
    history = []

    for index, page in enumerate(reference_string):
        hit = page in frames
        evicted = None

        if hit:
            last_used[page] = index

        else:
            if len(frames) < frame_count:
                frames.append(page)
            else:
                least_recent = min(
                    frames,
                    key=lambda p: last_used[p]
                )

                evicted = least_recent
                frames[frames.index(least_recent)] = page

            last_used[page] = index

        history.append({
            "page": page,
            "frames": frames.copy(),
            "hit": hit,
            "fault": not hit,
            "evicted": evicted
        })

    return history


def optimal(reference_string, frame_count):
    frames = []
    history = []

    for index, page in enumerate(reference_string):
        hit = page in frames
        evicted = None

        if not hit:
            if len(frames) < frame_count:
                frames.append(page)

            else:
                future = reference_string[index + 1:]

                next_use = {}

                for p in frames:
                    next_use[p] = (
                        future.index(p)
                        if p in future
                        else float("inf")
                    )

                victim = max(
                    frames,
                    key=lambda p: next_use[p]
                )

                evicted = victim
                frames[frames.index(victim)] = page

        history.append({
            "page": page,
            "frames": frames.copy(),
            "hit": hit,
            "fault": not hit,
            "evicted": evicted
        })

    return history
