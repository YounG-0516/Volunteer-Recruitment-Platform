/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2023-10-18 21:20:46                          */
/*==============================================================*/


-- drop trigger apply_time;

-- drop trigger approval_time;

-- drop procedure if exists activities_number;

-- drop
-- table if exists activity_Info;

-- drop
-- table if exists volunteer_Info;

-- drop index idx_end_time on activity;

-- drop index idx_start_time on activity;

/*==============================================================*/
/* Table: activity                                              */
/*==============================================================*/
create table activity
(
   av_id                char(10) not null,
   l_id                 char(10) not null,
   g_id                 char(10) not null,
   t_id                 char(10) not null,
   a_id                 char(10) not null,
   av_title             varchar(20) not null,
   av_state             varchar(10) not null,
   av_request           varchar(100) not null,
   av_content           varchar(100) not null,
   av_starttime         datetime not null,
   av_endtime           datetime not null,
   av_number            int not null,
   primary key (av_id)
);

/*==============================================================*/
/* Index: idx_start_time                                        */
/*==============================================================*/
create index idx_start_time on activity
(
   av_starttime
);

/*==============================================================*/
/* Index: idx_end_time                                          */
/*==============================================================*/
create index idx_end_time on activity
(
   av_endtime
);

/*==============================================================*/
/* Table: activity_type                                         */
/*==============================================================*/
create table activity_type
(
   t_id                 char(10) not null,
   t_name               varchar(20) not null,
   primary key (t_id)
);

/*==============================================================*/
/* Table: administrator                                         */
/*==============================================================*/
create table administrator
(
   a_id                 char(10) not null,
   i_id                 char(10) not null,
   a_pwd                varchar(20) not null,
   a_name               varchar(10) not null,
   primary key (a_id)
);

/*==============================================================*/
/* Table: apply                                                 */
/*==============================================================*/
create table apply
(
   ap_id                char(10) not null,
   v_id                 char(10) not null,
   av_id                char(10) not null,
   a_id                 char(10) not null,
   ap_time              datetime not null,
   ap_state             varchar(10) not null,
   ap_reason            varchar(100),
   ap_approvaltime      datetime,
   primary key (ap_id)
);

/*==============================================================*/
/* Table: ingroup                                               */
/*==============================================================*/
create table ingroup
(
   g_id                 char(10) not null,
   g_name               varchar(20) not null,
   primary key (g_id)
);

/*==============================================================*/
/* Table: institute                                             */
/*==============================================================*/
create table institute
(
   i_id                 char(10) not null,
   i_name               varchar(20) not null,
   primary key (i_id)
);

/*==============================================================*/
/* Table: location                                              */
/*==============================================================*/
create table location
(
   l_id                 char(10) not null,
   l_name               varchar(20) not null,
   primary key (l_id)
);

/*==============================================================*/
/* Table: volunteer                                             */
/*==============================================================*/
create table volunteer
(
   v_id                 char(10) not null,
   i_id                 char(10) not null,
   vg_id                char(10) not null,
   v_pwd                varchar(20) not null,
   v_name               varchar(10) not null,
   primary key (v_id)
);

/*==============================================================*/
/* Table: volunteerGroup                                        */
/*==============================================================*/
create table volunteerGroup
(
   vg_id                char(10) not null,
   vg_name              varchar(20) not null,
   vg_introduction      varchar(100),
   primary key (vg_id)
);

/*==============================================================*/
/* View: activity_Info                                          */
/*==============================================================*/
create VIEW  activity_Info
  as
select
    activity.av_id,
    activity.av_title,
    activity_type.t_name,
    activity.av_state,
    activity.av_request,
    activity.av_content,
    activity.av_starttime,
    activity.av_endtime,
    activity.av_number,
    location.l_name,
    ingroup.g_name
from
    activity,
    location,
    activity_type,
    ingroup
where
    activity.l_id = location.l_id and
    activity.g_id = ingroup.g_id and
    activity.t_id = activity_type.t_id;

/*==============================================================*/
/* View: volunteer_Info                                         */
/*==============================================================*/
create VIEW  volunteer_Info
  as
select
   volunteer.v_id,
   volunteer.v_name,
   institute.i_name,
   volunteerGroup.vg_name
from
   volunteer,
   institute,
   volunteerGroup
where
   volunteer.i_id = institute.i_id
   and volunteer.vg_id = volunteerGroup.vg_id;

alter table activity add constraint FK_activity_group foreign key (g_id)
      references ingroup (g_id) on delete restrict on update restrict;

alter table activity add constraint FK_activity_location foreign key (l_id)
      references location (l_id) on delete restrict on update restrict;

alter table activity add constraint FK_activity_type foreign key (t_id)
      references activity_type (t_id) on delete restrict on update restrict;

alter table activity add constraint FK_administrater_activity foreign key (a_id)
      references administrator (a_id) on delete restrict on update restrict;

alter table administrator add constraint FK_administrator_institute foreign key (i_id)
      references institute (i_id) on delete restrict on update restrict;

alter table apply add constraint FK_apply_activity foreign key (av_id)
      references activity (av_id) on delete restrict on update restrict;

alter table apply add constraint FK_apply_administrator foreign key (a_id)
      references administrator (a_id) on delete restrict on update restrict;

alter table apply add constraint FK_volunteer_apply foreign key (v_id)
      references volunteer (v_id) on delete restrict on update restrict;

alter table volunteer add constraint FK_volunteer_institute foreign key (i_id)
      references institute (i_id) on delete restrict on update restrict;

alter table volunteer add constraint FK_volunteer_volunteerGroup foreign key (vg_id)
      references volunteerGroup (vg_id) on delete restrict on update restrict;

DELIMITER $$
create procedure activities_number (IN p_volunteer_id char(10), OUT p_total_apply INT)
BEGIN
 SELECT apply.ap_id
 FROM apply, volunteer
 WHERE volunteer.v_id = p_volunteer_id
 AND volunteer.v_id = apply.v_id;
 
 SELECT COUNT(apply.ap_id)
 FROM apply, volunteer
 WHERE volunteer.v_id = p_volunteer_id
 AND volunteer.v_id = apply.v_id
 group by volunteer.v_id
 INTO p_total_apply;
END$$
DELIMITER ;

DELIMITER ;;
create trigger apply_time
    before insert on apply
    for each row 
    begin
        set new.ap_time = now();
    end;;
DELIMITER ;;

DELIMITER ;;
create trigger approval_time
    before update on apply
    for each row 
    begin
        set new.ap_approvaltime = now();
    end;;
DELIMITER ;;

