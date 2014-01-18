#ifndef _RUNGUARD_CONFIG_
#define _RUNGUARD_CONFIG_

/* Lots of suffixed names because we want to support multiple judgedaemons per host.  This allows 3 of them.*/
#define VALID_USERS "epsilon-judge-1,epsilon-judge-2,epsilon-judge-3"

#define CHROOT_PREFIX "/opt/epsilon/judge/judgings"

#define USE_CGROUPS 1

#endif /* _RUNGUARD_CONFIG_ */
