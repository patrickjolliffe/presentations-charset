// compile with: gcc -o extract extract.c -I$ORACLE_HOME/sdk/include -L$ORACLE_HOME -lclntsh
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <oci.h>

#define MAX_LEN 256

void checkerr(OCIError *errhp, sword status) {
    if (status != OCI_SUCCESS) {
        text errbuf[512];
        sb4 errcode = 0;
        memset(errbuf, 0, sizeof(errbuf));
        OCIErrorGet(errhp, 1, NULL, &errcode, errbuf, sizeof(errbuf), OCI_HTYPE_ERROR);
        fprintf(stderr, "OCI error (%d): %s\n", errcode, errbuf);
        exit(1);
    }
}

int main(int argc, char *argv[]) {
    OCIEnv *envhp = NULL;
    OCIError *errhp = NULL;
    OCISvcCtx *svchp = NULL;
    OCIStmt *stmthp = NULL;
    OCIDefine *defnp = NULL;
    OCIServer *srvhp = NULL;
    OCISession *authp = NULL;

    char *username = "pdbadmin";
    char *password = "pdbadmin";
    char *connect_str = "localhost:1521/freepdb1";

    char name[MAX_LEN];
    memset(name, 0, sizeof(name));
    char pattern[MAX_LEN];
    memset(pattern, 0, sizeof(pattern));

    OCIEnvCreate(&envhp, OCI_DEFAULT, 0, 0, 0, 0, 0, 0); // Can't use checkerr without errhp
    OCIHandleAlloc(envhp, (void **)&errhp, OCI_HTYPE_ERROR, 0, 0); // Cannot use checkerr yet
    checkerr(errhp, OCIHandleAlloc(envhp, (void **)&srvhp, OCI_HTYPE_SERVER, 0, 0));
    checkerr(errhp, OCIHandleAlloc(envhp, (void **)&svchp, OCI_HTYPE_SVCCTX, 0, 0));

    checkerr(errhp, OCIServerAttach(srvhp, errhp, (text *)connect_str, strlen(connect_str), OCI_DEFAULT));
    checkerr(errhp, OCIAttrSet(svchp, OCI_HTYPE_SVCCTX, srvhp, 0, OCI_ATTR_SERVER, errhp));

    checkerr(errhp, OCIHandleAlloc(envhp, (void **)&authp, OCI_HTYPE_SESSION, 0, 0));
    checkerr(errhp, OCIAttrSet(authp, OCI_HTYPE_SESSION, username, strlen(username), OCI_ATTR_USERNAME, errhp));
    checkerr(errhp, OCIAttrSet(authp, OCI_HTYPE_SESSION, password, strlen(password), OCI_ATTR_PASSWORD, errhp));
    checkerr(errhp, OCISessionBegin(svchp, errhp, authp, OCI_CRED_RDBMS, OCI_DEFAULT));
    checkerr(errhp, OCIAttrSet(svchp, OCI_HTYPE_SVCCTX, authp, 0, OCI_ATTR_SESSION, errhp));

    checkerr(errhp, OCIHandleAlloc(envhp, (void **)&stmthp, OCI_HTYPE_STMT, 0, 0));
    char sql[256];
    if (argc > 1) {
        snprintf(sql, sizeof(sql), "SELECT name FROM dogs WHERE name LIKE :pattern ORDER BY name");
    } else {
        snprintf(sql, sizeof(sql), "SELECT name FROM dogs ORDER BY name");
    }
    printf("Executing SQL: %s\n", sql);
    checkerr(errhp, OCIStmtPrepare(stmthp, errhp,
        (text *)sql, strlen(sql),
        OCI_NTV_SYNTAX, OCI_DEFAULT));
    if (argc > 1) {
        strncpy(pattern, argv[1], MAX_LEN - 1);
        printf("Binding pattern: '%s'\n", pattern);
        checkerr(errhp, OCIBindByName(stmthp, NULL, errhp, (text *)":pattern", -1, pattern, strlen(pattern) + 1, SQLT_STR, NULL, NULL, NULL, 0, NULL, OCI_DEFAULT));
    }
    checkerr(errhp, OCIStmtExecute(svchp, stmthp, errhp, 0, 0, NULL, NULL, OCI_DEFAULT));
    checkerr(errhp, OCIDefineByPos(stmthp, &defnp, errhp, 1, name, sizeof(name), SQLT_STR, NULL, NULL, NULL, OCI_DEFAULT));

    printf("NLS_LANG=%s\n", getenv("NLS_LANG"));
    while (OCIStmtFetch2(stmthp, errhp, 1, OCI_FETCH_NEXT, 0, OCI_DEFAULT) == OCI_SUCCESS) {
        printf("Good %s [", name);
        for (size_t i = 0; i < strlen(name); i++) {
            printf("%02x ", (unsigned char)name[i]);
        }
        printf("] (%zu bytes)\n", strlen(name));
    }

    return 0;
}