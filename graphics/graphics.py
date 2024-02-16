class Graphics:
  def display_logo(self):
    print('=====================')
    print('-----FAMILY FEUD-----')
    print('=====================\n')

  def display_main_menu(self):
    self.display_logo()
    print('AVAILABLE COMMANDS:')
    print('------------------')
    print('create server')
    print('join server')
    print('quit')
    print('------------------\n')

  def display_create_server_menu(self, host_info):
    self.display_logo()
    
    print('++++++++++++++++++')
    print('HOST: ', host_info['hostname'])
    print('IP: ', host_info['ip_address'])
    print('PORT: ', 58008)
    print('++++++++++++++++++\n')
    print('SET A PASSWORD FOR THE SERVER:')

  def display_join_server_menu(self, server_fields):
    self.display_logo()

    for key, val in server_fields.items():
      if val is not None:
        print(f'{key}: {val}')
      else:
        print(f'\nENTER {key}:')
        break
