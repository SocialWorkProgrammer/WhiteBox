import React from "react";
import { Disclosure, DisclosureButton, DisclosurePanel, Menu, MenuButton, MenuItem, MenuItems, } from "@headlessui/react";
import { Bars3Icon, BellIcon, XMarkIcon } from "@heroicons/react/24/outline";
import "../styles/main.css"
// navBar 링크 객체화
const tempURL = `http://localhost:3000/`

const navigation = [
    { name: '과실판단', href: tempURL, current: false },
    { name: '커뮤니티', href: tempURL, current: false },
]

function classNames(...classes) {
    return classes.filter(Boolean).join(" ");
}
function Header() {
    return (
        <Disclosure as="nav" className="nav-bar" >
        <div className="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
            <div className="relative flex h-16 items-center justify-between">
                {/* 모바일 버전 */}
            <div className="absolute inset-y-0 left-0 flex items-center sm:hidden">
                <DisclosureButton className="group relative inline-flex items-center justify-center rounded-md p-2 text-gray-400 hover:bg-gray-700 hover:text-white focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white">
                <span className="absolute -inset-0.5" />
                <span className="sr-only">메인메뉴</span>
                <Bars3Icon
                    aria-hidden="true"
                    className="block h-6 w-6 group-data-[open]:hidden"
                />
                <XMarkIcon
                    aria-hidden="true"
                    className="hidden h-6 w-6 group-data-[open]:block"
                />
                </DisclosureButton>
            </div>
            {/* 로고와 네비게이션 링크 */}
            <div className="flex flex-1 items-left justify-left sm:items-stretch sm:justify-start">
                {/* 로고 */}
                <div className="flex flex-shrink-0 items-center">
                <img
                    alt=""
                    src="https://picsum.photos/250/250"
                    className="h-8 w-auto"
                />
                </div>
                {/* 네비게이션 링크 -> 화면 줄어들면 없어짐 */}
                <div className="hidden sm:ml-6 sm:block">
                <div className="flex space-x-4">
                    {navigation.map((item) => (
                    <a
                        key={item.name}
                        href={item.href}
                        aria-current={item.current ? "page" : undefined}
                        className={classNames(
                        item.current
                            ? "bg-gray-900 text-white"
                            : "text-white hover:bg-gray-700 hover:text-gray",
                        "rounded-md px-3 py-2 text-sm font-medium"
                        )}
                    >
                        {item.name}
                    </a>
                    ))}
                </div>
                </div>
            </div>
            {/* 알림과 프로필 */}
            <div className="absolute inset-y-0 right-0 flex items-center pr-2 sm:static sm:inset-auto sm:ml-6 sm:pr-0">
                {/* 알림 */}
                <button
                type="button"
                className="relative rounded-full bg-gray-800 p-1 text-gray-400 hover:text-white focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800"
                >
                <span className="absolute -inset-1.5" />
                <span className="sr-only">알림</span>
                <BellIcon aria-hidden="true" className="h-6 w-6" />
                </button>

                {/* 프로필 */}
                <Menu as="div" className="relative ml-3">
                <div>
                    <MenuButton className="relative flex rounded-full bg-gray-800 text-sm focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800">
                    <span className="absolute -inset-1.5" />
                    <span className="sr-only">프로필</span>
                    <img
                        alt=""
                        src="https://picsum.photos/249/249"
                        className="h-8 w-8 rounded-full"
                    />
                    </MenuButton>
                </div>
                {/* 드롭다운 메뉴 아이템들 */}
                <MenuItems
                    transition
                    className="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5 transition focus:outline-none data-[closed]:scale-95 data-[closed]:transform data-[closed]:opacity-0 data-[enter]:duration-100 data-[leave]:duration-75 data-[enter]:ease-out data-[leave]:ease-in"
                >
                    <MenuItem>
                    <a
                        href="#"
                        className="block px-4 py-2 text-sm text-gray-700 data-[focus]:bg-gray-100"
                    >
                        프로필 보기
                    </a>
                    </MenuItem>
                    <MenuItem>
                    <a
                        href="#"
                        className="block px-4 py-2 text-sm text-gray-700 data-[focus]:bg-gray-100"
                    >
                        로그아웃
                    </a>
                    </MenuItem>
                    <MenuItem>
                    <a
                        href="#"
                        className="block px-4 py-2 text-sm text-gray-700 data-[focus]:bg-gray-100"
                    >
                        회원탈퇴
                    </a>
                    </MenuItem>
                </MenuItems>
                </Menu>
            </div>
            </div>
        </div>

        {/* 작은 화면인 경우 */}
        <DisclosurePanel className="sm:hidden">
            <div className="space-y-1 px-2 pb-3 pt-2">
            {navigation.map((item) => (
                <DisclosureButton
                key={item.name}
                as="a"
                href={item.href}
                aria-current={item.current ? "page" : undefined}
                className={classNames(
                    item.current
                    ? "bg-gray-900 text-white"
                    : "text-gray-300 hover:bg-gray-700 hover:text-white",
                    "block rounded-md px-3 py-2 text-base font-medium"
                )}
                >
                {item.name}
                </DisclosureButton>
            ))}
            </div>
        </DisclosurePanel>
        </Disclosure>
    );
}

export default Header;
