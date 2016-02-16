import mysql.connector as sqlCon
import config
def DBConnection():
    return sqlCon.connect(user=config.user,password= config.password, host=config.host, database = config.database)
def queryMaker(cursor, args, table, conditions=None):
    project = ''
    for arg in args:
        project += arg+", "
    project = project[:-2]+ " "
    query = ("SELECT "+ project+ "FROM "+ table)
    if conditions is not None:
        query += ' '+conditions
    #print 'query is ',query
    cursor.execute(query)


cnx = DBConnection()

cursor = cnx.cursor()
queryMaker(cursor,['id'],"Intents")
for id in cursor:
    components= []
    print 'Starting rendering process for Intent:',id[0]
    IActionConnection = DBConnection()
    IActionCursor = IActionConnection.cursor()
    queryMaker(IActionCursor, ['action'],'IActions', 'WHERE intent_id = '+str(id[0]))
    for action in IActionCursor:
        print '****Action ',action[0], "is being considered"
        IFActionConnection = DBConnection()
        IFCursor = IFActionConnection.cursor()
        queryMaker(IFCursor,['filter_id'],'IFActions','WHERE action = '+str(action[0]))
        for filter_id in IFCursor:
            print '******** Filter ID ',filter_id[0]
            IntentFilterConnection = DBConnection()
            IntentFilterCursor = IntentFilterConnection.cursor()
            queryMaker(IntentFilterCursor,['component_id'],'IntentFilters','WHERE id = '+str(filter_id[0]))
            for component_id in IntentFilterCursor:
                if component_id[0] in components:
                    continue
                components.append(component_id[0])
                print "**********Component ",component_id[0]," found"
                LinksConnection = DBConnection()
                LinksCursor = LinksConnection.cursor()
                query = 'INSERT INTO Links (id, intent_id, component_id, type, reserved) VALUES (NULL, \''+str(id[0])+'\', \''+str(component_id[0])  + '\',0, NULL)'
                print query+"++++++++"
                LinksCursor.execute(query)
                LinksConnection.commit()
                LinksCursor.close()
                LinksConnection.close()
            IntentFilterCursor.close()
            IntentFilterConnection.close()
        IFCursor.close()
        IFActionConnection.close()

    IActionCursor.close()
    IActionConnection.close()
cursor.close()
cnx.close()