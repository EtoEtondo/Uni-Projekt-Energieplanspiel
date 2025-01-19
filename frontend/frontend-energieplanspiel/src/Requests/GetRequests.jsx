export const fetchInstitutions = async () => {
  return fetch("http://localhost:8000/institution/", {
    method: "GET",
    header: {
      "Content-Type": "application/json",
    },
    // mode: "cors",
    credentials: "include",
  }).then(async (response) => {
    const data = await response.json();
    if (response.ok) {
      if (Object.keys(data).length > 0) {
        const institutions = [];
        Object.keys(data).map((id, index) =>
          institutions.push({
            name: data[id].name,
            id: Object.keys(data)[index],
          })
        );
        return { status: -1, data: institutions};
      } else {
        return { status: -1, data: [] };
      }
    } else {
      return { status: 1, data: [], message: data["Error"]};
    }
  });
};

export const fetchInstructors = async (id) => {
  return fetch("http://localhost:8000/instructor/?institution=" + id, {
    method: "GET",
    header: {
      "Content-Type": "application/json",
    },
    // mode: "cors",
    credentials: "include",
  }).then(async (response) => {
    const data = await response.json();
    if (response.ok) {
      if (Object.keys(data).length > 0) {
        const instructors = [];
        Object.keys(data).map((id, index) =>
          instructors.push({
            username: data[id].username,
            name: data[id].display_name,
            enabled: data[id].enabled,
            id: Object.keys(data)[index],
          })
        );

        return { status: -1, data: instructors };
      } else {
        return { status: -1, data: [] };
      }
    } else {
      return { status: 1, data: [], message: data["Error"]};
    }
  });
};

export const fetchSchedule = async (id) => {
  return fetch("http://localhost:8000/schedule/?username=" + id, {
    method: "GET",
    header: {
      "Content-Type": "application/json",
    },
    // mode: "cors",
    credentials: "include",
  }).then(async (response) => {
    const data = await response.json();
    if (response.ok) {
      if (Object.keys(data).length > 0) {
        const schedules = [];
        Object.keys(data).map((id, index) =>
          schedules.push({
            name: data[id].timeslot.split("T")[0],
            id: Object.keys(data)[index],
          })
        );
        return { status: -1, data: schedules };
      } else {
        return { status: -1, data: [] };
      }
    } else {
      return { status: 1, data: [], message: data["Error"]};
    }
  });
};

export const fetchGroups = async (id) => {
  return fetch("http://localhost:8000/group/?schedule=" + id, {
    method: "GET",
    header: {
      "Content-Type": "application/json",
    },
    // mode: "cors",
    credentials: "include",
  }).then(async (response) => {
    const data = await response.json();
    if (response.ok) {
      if (Object.keys(data).length > 0) {
        const groups = [];
        Object.keys(data).map((id, index) =>
          groups.push({
            name: data[id].display_name,
            username: data[id].username,
            enabled: data[id].enabled,
            has_submitted: data[id].has_submitted,
            id: Object.keys(data)[index],
            calc_running: data[id].calc_running,
            results_exist: data[id].results_exist,
          })
        );
        return { status: -1, data: groups };
      } else {
        return { status: -1, data: [] };
      }
    } else {
      return { status: 1, data: [], message: data["Error"]};
    }
  });
};

export const fetchInfo = async () => {
  return fetch("http://localhost:8000/info/", {
    method: "GET",
    header: {
      "Content-Type": "application/json",
    },
    // mode: "cors",
    credentials: "include",
  }).then(async (response) => {
    const data = await response.json();
    if (response.ok) {
      return { status: -1, data: data }
    } else {
      return { status: 1, data: []};
    }
  });
};

export const fetchProgress = async (id) => {
  return fetch('http://localhost:8000/progress/?schedule=' + id, {
    method: 'GET',
    // mode: "cors",
    credentials: 'include',
  }).then(async (response) => {
    const data = await response.json();
    if (response.ok) {
      return { status: -1, data: data }
    } else {
      return { status: 1, message: data["Error"]};
    }
  });
};


export const fetchResults = async (id) => {
  return fetch('http://localhost:8000/results/?schedule=' + id, {
    method: 'GET',
    header: {
      'Content-Type': 'application/json',
    },
    // mode: "cors",
    credentials: 'include',
  }).then(async (response) => {
    const data = await response.json();
    if (response.ok) {
      return { status: -1, data: data }
    } else {
      return { status: 1, data: [], message: data["Error"]};
    }
  });
};
