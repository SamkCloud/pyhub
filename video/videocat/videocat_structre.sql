CREATE TABLE IF NOT EXISTS file_list (
	film_id integer primary key autoincrement,
	filename TEXT,
	path TEXT,
	filesize int,
	Container TEXT,
	duration int,
	Acodec TEXT,
	Vcodec TEXT, 
	Xsize int,
	Ysize int,
	bitrate int
	)
	


