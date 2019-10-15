import { Model } from '@vuex-orm/core'

export default class User extends Model {
  static entity = 'usersEntities'

  static fields () {
    return {
      id: this.attr(null),
      email: this.attr(''),
      first_name: this.attr(''),
      last_name: this.attr(''),
      is_admin: this.attr(''),
    }
  }
}
