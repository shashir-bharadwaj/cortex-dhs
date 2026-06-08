export const tokenStorage = {
  getAccessToken: () => localStorage.getItem("access_token"),
  getRefreshToken: () => localStorage.getItem("refresh_token"),

  setTokens: (accessToken: string, refreshToken?: string) => {
    localStorage.setItem("access_token", accessToken);
    if (refreshToken) {
      localStorage.setItem("refresh_token", refreshToken);
    }
  },

  clear: () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
  },
};