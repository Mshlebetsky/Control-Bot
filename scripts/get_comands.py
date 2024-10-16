def get_comands():
    file = open('Data/comands.txt','r',encoding='utf-8')
    comands = []
    description = []
    for line in file:
        print(line)
        comands.append(line.split('-')[0].replace(' ',''))

        description.append(line.split('-')[1].replace('\n',''))
    return comands, description

def get_help():
    show_comands = ''
    arr = get_comands()
    for i, j in enumerate(arr[0]):
        temp_line = f'/{j} - {arr[1][i]}\n'
        show_comands += temp_line
    return show_comands