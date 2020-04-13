function getTimeElapsed(start: string | number, strDateTime: string | number): string {
  const t1 = new Date(start).getTime(),
    t2 = new Date(strDateTime).getTime();
  if (!t1 || !t2 || isNaN(t1) || isNaN(t2)) return "";
  let milliseconds = Math.abs(t1 - t2);
  const msInHour = 1000 * 60 * 60;
  const portions: string[] = [];

  const hours = Math.trunc(milliseconds / msInHour);
  if (hours > 0) {
    portions.push(String(hours).padStart(2, "0"));
    milliseconds = milliseconds - hours * msInHour;
  } else {
    portions.push("00");
  }

  const msInMinute = 1000 * 60;
  const minutes = Math.trunc(milliseconds / msInMinute);
  if (minutes > 0) {
    portions.push(String(minutes).padStart(2, "0"));
    milliseconds = milliseconds - minutes * msInMinute;
  } else {
    portions.push("00");
  }

  const seconds = Math.trunc(milliseconds / 1000);
  portions.push(String(seconds).padStart(2, "0"));

  return portions.join(":");
}

function shorten(text: string, len?: number): string {
  const defaultLength = 32;
  if (!text) return "";
  if (text.length > (len || defaultLength)) {
    return text.substr(0, len || defaultLength) + "...";
  } else {
    return text;
  }
}

function getErrorMessage(statusCode?: number): string {
  const errorMessages: { [key: number]: string } = {
    403: "この操作は許されていません。一旦ログアウトし、再度ログインしてからお試しください。",
    500: "サーバー内部でエラーが発生しました。しばらくしてからアクセスしてください。"
  };

  if (statusCode) {
    return errorMessages[statusCode] || "正しく処理することができませんでした。管理者へお問い合わせください。";
  }
  return "サーバーにアクセスできませんでした。インターネット接続を確認し、管理者へお問い合わせください。";
}

function scrollToElementById(id: string) {
  const ref = document.getElementById(id)
  if (ref) ref.scrollIntoView({
    behavior: "smooth"
  });
}

export {
  getTimeElapsed,
  shorten,
  getErrorMessage,
  scrollToElementById
}