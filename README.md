# Code4Teens REST API

## Deploy on Google Cloud Run
```sh
$ gcloud run deploy --source .
$ gcloud run services update <service-name> \
    --add-cloudsql-instances <connection-name> \
    --set-env-vars SECRET_KEY=<secret-key>,\
      MYSQL_CONNECTION=<connection-name>,\
      MYSQL_USERNAME=<username>,\
      MYSQL_PASSWORD=<password>,\
      MYSQL_DATABASE=<database>
```

## Database Schema

### User
```sql
CREATE TABLE `user` (
  `id` bigint(20) unsigned NOT NULL,
  `password` char(60) DEFAULT NULL,
  `name` varchar(64) NOT NULL,
  `discriminator` char(4) NOT NULL,
  `display_name` varchar(64) NOT NULL,
  `xp` int(11) NOT NULL DEFAULT '0',
  `is_admin` tinyint(1) NOT NULL DEFAULT '0',
  `api_key` char(43) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_updated` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`,`discriminator`),
  CONSTRAINT `user_chk_1` CHECK ((length(`id`) = 18)),
  CONSTRAINT `user_chk_2` CHECK ((length(`discriminator`) = 4))
)
```

### Bot
```sql
CREATE TABLE `bot` (
  `id` bigint(20) unsigned NOT NULL,
  `name` varchar(64) DEFAULT NULL,
  `discriminator` char(4) DEFAULT NULL,
  `display_name` varchar(64) DEFAULT NULL,
  `user_id` bigint(20) unsigned NOT NULL,
  `cohort_id` smallint(5) unsigned NOT NULL,
  `msg_id` bigint(20) unsigned NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_updated` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `msg_id` (`msg_id`),
  UNIQUE KEY `name` (`name`,`discriminator`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `bot_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `bot_chk_1` CHECK ((length(`id`) = 18)),
  CONSTRAINT `bot_chk_2` CHECK ((length(`msg_id`) = 18)),
  CONSTRAINT `bot_chk_3` CHECK ((length(`discriminator`) = 4))
)
```

### Channel
```sql
CREATE TABLE `channel` (
  `id` bigint(20) unsigned NOT NULL,
  `name` varchar(64) NOT NULL,
  `user_id` bigint(20) unsigned NOT NULL,
  `cohort_id` smallint(5) unsigned NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_updated` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`cohort_id`),
  CONSTRAINT `channel_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `channel_chk_1` CHECK ((length(`id`) = 18))
)
```

### Cohort
```sql
CREATE TABLE `cohort` (
  `id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `nickname` varchar(16) NOT NULL,
  `duration` tinyint(3) unsigned NOT NULL,
  `start_date` date NOT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `review_schema` json DEFAULT NULL,
  `feedback_schema` json DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `is_active` (`is_active`)
)
```

### Enrolment
```sql
CREATE TABLE `enrolment` (
  `id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint(2) unsigned NOT NULL,
  `cohort_id` smallint(5) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`cohort_id`),
  KEY `cohort_id` (`cohort_id`),
  CONSTRAINT `enrolment_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `enrolment_ibfk_2` FOREIGN KEY (`cohort_id`) REFERENCES `cohort` (`id`)
)
```

### Eval
```sql
CREATE TABLE `eval` (
  `id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `evaluator_id` bigint(20) unsigned NOT NULL,
  `evaluatee_id` bigint(20) unsigned NOT NULL,
  `cohort_id` smallint(5) unsigned NOT NULL,
  `date` date NOT NULL,
  `review` json DEFAULT NULL,
  `feedback` json DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `evaluator_id` (`evaluator_id`,`evaluatee_id`,`cohort_id`,`date`),
  KEY `evaluatee_id` (`evaluatee_id`),
  KEY `cohort_id` (`cohort_id`),
  CONSTRAINT `eval_ibfk_1` FOREIGN KEY (`evaluator_id`) REFERENCES `user` (`id`),
  CONSTRAINT `eval_ibfk_2` FOREIGN KEY (`evaluatee_id`) REFERENCES `user` (`id`),
  CONSTRAINT `eval_ibfk_3` FOREIGN KEY (`cohort_id`) REFERENCES `cohort` (`id`)
)
```

### Subscription
```sql
CREATE TABLE `subscription` (
  `id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `email` varchar(64) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
)
```
