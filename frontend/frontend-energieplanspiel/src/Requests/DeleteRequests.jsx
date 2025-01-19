export const deleteInstitution = async (id) => {
    return fetch("http://localhost:8000/institution/", {
      method: "DELETE",
      header: {
        "Content-Type": "application/json",
      },
      // mode: "cors",
      credentials: "include",
      body: JSON.stringify({
        institution: id,
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

  export const deleteInstructor = async (username, id) => {
    return fetch("http://localhost:8000/instructor/?institution=" + id, {
      method: "DELETE",
      header: {
        "Content-Type": "application/json",
      },
      // mode: "cors",
      credentials: "include",
      body: JSON.stringify({
        username: username,
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

  export const deleteSchedule = async (id) => {
    return fetch("http://localhost:8000/schedule/?id=" + id, {
      method: "Delete",
      header: {
        "Content-Type": "application/json",
      },
      // mode: "cors",
      credentials: "include",
      body: JSON.stringify({
        schedule: id
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

  export const deleteGroup = async (username) => {
    return fetch("http://localhost:8000/group/?username=" + username, {
      method: "Delete",
      header: {
        "Content-Type": "application/json",
      },
      // mode: "cors",
      credentials: "include",
      body: JSON.stringify({
        username: username,
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