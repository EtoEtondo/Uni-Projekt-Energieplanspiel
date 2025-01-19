export const editInstructor = async (editEntry) => {
    return fetch("http://localhost:8000/instructor/", {
      method: "PUT",
      header: {
        "Content-Type": "application/json",
      },
      // mode: "cors",
      credentials: "include",
      body: JSON.stringify({
        password: editEntry.password,
        enabled: editEntry.enabled,
        username: editEntry.username
      }),
    }).then(async (response) => {
      const data = await response.json();
      if (response.ok) {
          return { status: 0, message:data["Success"]};
      } else {
        return { status: 1, message:data["Error"]};
      }
    });
  };

  export const editGroup = async (editEntry) => {
    return fetch("http://localhost:8000/group/", {
      method: "PUT",
      header: {
        "Content-Type": "application/json",
      },
      // mode: "cors",
      credentials: "include",
      body: JSON.stringify({
        password: editEntry.password,
        username: editEntry.username
      }),
    }).then(async (response) => {
      const data = await response.json();
      if (response.ok) {
        return { status: 0, message:data["Success"]};
      } else {
        return { status: 1, message:data["Error"]};
      }
    });
  };

  export const editAccess = async (id) => {
    return fetch('http://localhost:8000/result_access/', {
      method: 'PUT',
      header: {
        'Content-Type': 'application/json',
      },
      // mode: "cors",
      credentials: 'include',
      body: JSON.stringify({
            schedule: id,
            result_access: true,
      })
    }).then(async (response) => {
      const data = await response.json();
      if (response.ok) {
        return { status: 0, message:data["Success"]};
      } else {
        return { status: 1, message:data["Error"]};
      }
    });
  };

  