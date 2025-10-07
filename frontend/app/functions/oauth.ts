const handleGithubLogin = () => {
  const authWindow = window.open(
    "http://127.0.0.1:8080/services/github/index",
    "GitHub Login",
    "width=600,height=700",
  );

  window.addEventListener("message", (event) => {
    if (event.data.type === "github_login_complete") {
      console.log("GitHub login finished. Cookie should now be set.");
      window.location.href = "/explore";
    }
  });
};

export async function redirectOauthGithub() {
  try {
    handleGithubLogin();
  } catch (err) {
    console.log("Error: ", err);
  }
}

const handleTodoistLogin = () => {
  const authWindow = window.open(
    "http://127.0.0.1:8080/services/todoist/index",
    "GitHub Login",
    "width=600,height=700",
  );

  window.addEventListener("message", (event) => {
    if (event.data.type === "todoist_login_complete") {
      console.log("Todoist login finished. Cookie should now be set.");
      window.location.href = "/explore";
    }
  });
};

export async function redirectOauthTodoist() {
  try {
    handleTodoistLogin();
  } catch (err) {
    console.log("Error: ", err);
  }
}
