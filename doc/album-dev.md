This document define the html format for album page.

Applied for both backend and frontend.

## Data model for image
an image represented by database has the below attribute:

* `idx` -- unique id for each pic
* `img_url` -- url for image
* `thumb_url` -- url for image thumb
* `desc` -- a brief introduction to the pic

## web api
### /admin/uploadimg
* post files to this api
* response is in JSON format

response:
```
{
	"img_name_1": { # success example
		"status": true,
		"idx": IMG_IDX,
		"img_url": IMG_URL,
		"thumb_url": THUMB_URL,
	},
	"img_name_2": { # failed example
		"status": false,
		"msg": ERROR_MSG,
	}
}
```
### /admin/imginfo
* support POST request
* all the data in JSON format

request:

```
{
	"ID1": {
		'action': 'write'/'read',
		'desc': IMG_DESC, # requred for write opeartion
	},
	"ID2": ...
}
```

response:

```
{
	"ID1": {
		'status': true/false, # true -- success, false -- failure
		'msg': MSG_FOR_FAIL, # only show msg when status == false
		# below fields is for 'read' option
		'img_url': IMG_URL,
		'thumb_url': THUMB_URL,
		'desc': IMG_DESC,
	},
	"ID2": ...
}
```

## raw format defination for album
When someone want to post a album page to database, he needs to give

* `album-desc` -- an introduction to this photo album
* several images under `album-images`
* assign a pic as cover (`data-cover`)

```html
<div id="album-desc">
image desc here
</div>

<div id="album-images" data-cover="[cover_id]">
	<img data-id="[ImageID1]" />
	<img data-id="[ImageID2]" />
	...
</div>
```

## html struct after being converted.
```html
<div id="album-cover">
	<img src="cover_thumb" alt="desc" data-id="[ImageID]" data-src="srcurl" />
</div>

<div id="album-desc">
	image desc here
</div>

<div id="album-images" data-cover="[cover_id]">
	<img src="thumb" alt="desc" data-id="[ImageID1]" data-src="src" />
	...
</div>
```
