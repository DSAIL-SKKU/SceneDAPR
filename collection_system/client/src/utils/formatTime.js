import moment from 'moment';

// ----------------------------------------------------------------------

export function getKoreaTime(dataString) {
  // SQLite에서 가져온 시간을 한국 시간으로 변환 (UTC -> KST = UTC + 9)
  // Input 예시: 2021-05-18T09:00:00.000Z

  const kst = moment(dataString).utcOffset(9).format('YYYY-MM-DD HH:mm');

  return kst;
}

export function calculateElapsedTime(startTime, endTime) {
  const elapsedTime = endTime - startTime;
  const minutes = Math.floor(elapsedTime / 60000);
  const seconds = ((elapsedTime % 60000) / 1000).toFixed(0);
  return `${minutes}분 ${seconds}초`;
}