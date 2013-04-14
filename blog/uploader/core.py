from blog.models import Image


class Uploader():
    def __init__(self):
        from Queue import Queue
        import threading
        self.queue = Queue()
        self.th = threading.Thread(target=self._monitor)

    def _monitor(self):
        from imgur import upload
        while 1:
            image = self.queue.get()
            try:
                img_url, thumb_url = upload(image.img.read())
                Image.objects.filter(idx=image.idx).update(
                    _img_url=img_url, _thumb_url=thumb_url)
            except:
                pass

    def daemon(self):
        from django.db.models.signals import post_save
        from django.dispatch import receiver

        @receiver(post_save, sender=Image, created=True)
        def handler(sender, **kwargs):
            image = kwargs.get('instance')
            self.queue.put(image)

        self.th.start()
