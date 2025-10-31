/*
 ** EPITECH PROJECT, 2025
 ** Area_Mirroring
 ** File description:
 ** Warning
 */

export default function Warning(title: string, message: string) {
  return (
    <div className="bg-yellow-100 border border-yellow-400 text-yellow-800 px-4 py-3 rounded relative">
      {title && <strong className="font-bold">{title}: </strong>}
      <span className="block sm:inline">{message}</span>
    </div>
  )
}
