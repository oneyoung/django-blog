import logging
from Queue import Queue
from blog.models import Blog, Image
from imgur import upload

logger = logging.getLogger(__name__)


class Uploader():
    def __init__(self):
        import threading
        self.Q = Queue()
        self.th = threading.Thread(target=self._thread_handler, args=(self))

    def _thread_handler(self):
        blogs2update = set()
        while 1:
            try:
                image = self.Q.get(block=True, timeout=10)
                logger.debug("queue get " + repr(image))
                try:
                    img_url, thumb_url = upload(image.img.read())
                    # use update specified fields to avoid concurrency issue
                    Image.objects.filter(idx=image.idx).update(
                        _img_url=img_url, _thumb_url=thumb_url, status='uploaded')
                    # make sure we got a newest copy
                    new_image = image.objects.get(idx=image.idx)
                    if new_image.blog_id:
                        blogs2update.add(new_image.blog_id)
                except:
                    logger.exception()
            except Queue.Empty:
                for blog_id in blogs2update:
                    try:
                        blog = Blog.objects.get(pk=blog_id)
                        blog.save()
                        blog.image_set.update(status='updated')
                    except:
                        logger.exception()
                break

    def _queue(self, obj):
        if not self.th.is_alive():
            self.th.start()
        logger.debug("queue put " + repr(obj))
        self.Q.put(obj)

    def _scan(self):
        for image in Image.objects.exclude(status='updated').execlude(blog=None):
            self._queue(image)

    def start(self):
        from django.db.models.signals import post_save
        from django.dispatch import receiver

        @receiver(post_save, sender=Image, created=True)
        def handler(sender, **kwargs):
            image = kwargs.get('instance')
            self._queue(image)

        self._scan()
