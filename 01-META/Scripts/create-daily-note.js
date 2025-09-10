module.exports = async (tp) => {
  const year = tp.date.now("YYYY");
  const month = tp.date.now("MM");
  const day = tp.date.now("DD");

  const folder = `Daily/${year}/${month}/${day}`;
  const file = `${day}.md`;

  // Tạo note từ template
  return tp.file.create_new(
    tp.file.find_tfile("DailyNote.md"),
    file,
    false,
    folder
  );
}
