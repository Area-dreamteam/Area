import Link from "next/link";

export default function Login() {
    return (
        <section className="min-h-screen bg-[url('/BackGround_Rotate.jpg')] bg-cover bg-center flex flex-col items-center justify-center p-10">
        <div className="w-full max-w-sm p-10 bg-white/70 rounded-[45px]">
            <h2 className="text-5xl font-bold mb-8 font-extrabold text-center text-[#F18585] font-[Montserrat]">
                LOGIN
            </h2>
                <input
                    type="email"
                    placeholder="Email"
                    className="w-full mb-6 p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#F18585]"
                />
                <div className="relative mb-4">
                    <input
                        placeholder="Password"
                        className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#F18585]"
                    />
                    <button
                        type="button"
                        className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-500"
                    >
                    </button>
                </div>
                <Link href={`/login`}>
                  <button
                    className="w-full bg-[#F18585] hover:bg-[#e07070] text-white font-extrabold py-3 rounded-lg cursor-pointer"
                  >Login</button>
                </Link>
                <Link href={`/register`}>
                    <button className="w-full bg-[#F18585] hover:bg-[#e07070] text-white cursor-pointer"
                    >Register</button>
                </Link>
            </div>
        </section>
    );
}
