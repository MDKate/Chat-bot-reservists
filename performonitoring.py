from googleDrive import list_folder_to_drive
import pandas as pd

async def performance_monitoring():
    root_folder_id = '1Sl2sM5Mi76sOKr2e0VTIxu5_BcTSmtVG'
    df = await list_folder_to_drive(root_folder_id)
    df['folder'] = 'Зачтено'
    if len(df) >= 1:
        df['reload'] = df['name'].str.contains('reload').astype(int)
        del(df['id'])
        df.reset_index(inplace=True)
        df['delete'] = ''
        df.sort_values(by='name', ascending=False)
        df['name'] = df['name'].str.replace('_reload', '')
        for i in range(0, len(df)):
            if df['reload'][i] == 0 and len(df[df['name'] == df['name'][i]]['name'].values) == 2:
                df['delete'][i] = 'del'
        df = df[df['delete'] != 'del']
        del(df['delete'])
        del(df['index'])


    root_folder_id = '1jnqQyb3itTriDg6y61o01dYNlRmyRVmM'
    df1 = await list_folder_to_drive(root_folder_id)
    df1['folder'] = 'Не зачтено'
    if len(df1) >= 1:
        df1['reload'] = df1['name'].str.contains('reload').astype(int)
        del(df1['id'])
        df1.reset_index(inplace=True)
        df1['delete'] = ''
        df1.sort_values(by='name', ascending=False)
        df1['name'] = df1['name'].str.replace('_reload', '')
        for i in range(0, len(df1)):
            if df1['reload'][i] == 0 and len(df1[df1['name'] == df1['name'][i]]['name'].values ) == 2:
                df1['delete'][i] = 'del'
        df1 = df1[df1['delete'] != 'del']
        del(df1['delete'])
        del(df1['index'])
    if len(df) < 1 and len(df1) < 1:
        df = ""
    elif len(df) < 1 and len(df1) >= 1:
        df = df1
    elif len(df) >= 1 and len(df1) >= 1:
        df = pd.concat([df, df1], ignore_index=True)
    try:
        df['name'] = df['name'].str.replace('.docx', '')
    except:
        pass
    return df