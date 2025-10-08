import { Link, useLocation } from 'react-router-dom'

const navItems = [
    {name: 'Dashboard', path: '/' },
    {name: 'Hosts', path: '/hosts' },
    {name: 'Alerts', path: '/alerts' },
    {name: 'Metrics', path: '/metrics'},
]

export default function Sidebar() {
    const { pathname } = useLocation()

    return (
        <div className="w-64 bg-white shadow h-full">
            <div className="p-6 font-bold text-xl border-b">Infra-Watch</div>
            <nav className="flex flex-col p-4 space-y-2">
                {navItems.map(item => (
                    <Link
                        key={item.name}
                        to={item.path}
                        className={`p-2 rounded ${
                            pathname === item.path
                            ? 'bg-blue-500 text-white' 
                            : 'hover:bg-gray-200'
                        }`}
                    >
                        {item.name}
                    </Link>
                ))}
            </nav>
        </div>
    )
}