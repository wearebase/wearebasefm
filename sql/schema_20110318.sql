DROP TABLE IF EXISTS `settings`;

CREATE TABLE `settings` (
  `id` int(11) default NULL,
  `name` varchar(64) default NULL,
  `value` varchar(128) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `tracks`;

CREATE TABLE `tracks` (
  `id` int(11) NOT NULL auto_increment,
  `artist` varchar(64) default NULL,
  `title` varchar(64) default NULL,
  `played_on` timestamp NULL default NULL,
  `link` varchar(128) default NULL,
  `short_link` varchar(32) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;