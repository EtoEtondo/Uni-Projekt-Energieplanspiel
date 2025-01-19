

export const delay = async (timeout) => {
    return new Promise((resolve) => {
      setTimeout(resolve, timeout);
    });
  };

  export const waitAnimation = async (runStateobj) => {
    while (runStateobj.current.isAnimationActive) {
      await delay(10);
    }
    return Promise.resolve();
  };