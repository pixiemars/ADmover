import pyad.adquery
import cli.app

def add_to_group(username, password, server, groupdn, cn):
    from pyad import pyad
    pyad.set_defaults(ldap_server=server,
                      username=username, password=password)
    group = pyad.from_dn(groupdn)
    print group
    user = pyad.from_cn(cn)
    print user
    group.add_members([user])


def search_and_move(attribute, value, dn, un, pw, server, groupdn):
    q = pyad.adquery.ADQuery()
    q.execute_query(
        attributes=["cn", "description"],
        where_clause=attribute + "= '" + value + "'",
        base_dn=dn
    )
    for row in q.get_results():
        print row["cn"]
        cn = row["cn"]
        add_to_group(un, pw, server, groupdn, cn)


@cli.app.CommandLineApp
def admove(app):
    a = app.params.attribute
    v = app.params.value
    d = app.params.DN
    u = app.params.username
    p = app.params.password
    s = app.params.server
    gdn = app.params.groupdn
    search_and_move(a, v, d, u, p, s, gdn)

admove.add_param("username", help="AD Username", default="", type=str)

admove.add_param("password", help="AD Password",
                 default="", type=str)

admove.add_param("server",
                 help="AD Server Address", default="", type=str)

admove.add_param("groupdn",
                 help="DN of Group you are adding to", default="",
                 type=str)

admove.add_param("attribute",
                 help="AD Attribute you are searching eg: department",
                 default="",
                 type=str)

admove.add_param("value", help="Value of attribute you are searching",
                 default="", type=str)

admove.add_param("DN", help="Distinguished name you are searching",
                 default="", type=str)

if __name__ == "__main__":
    admove.run()
