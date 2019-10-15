export const state = () => {
  return {
    token: null,
    user: null,
    is_authenticated: false,
  }
}
export const mutations = {
  setAuth (state, token) {
      state.token = token;
  },
  setUser (state, data) {
      state.user = data;
      state.is_authenticated = true
  },
  removeUser (state) {
      state.user = null;
      state.is_authenticated = false;
  }
}
