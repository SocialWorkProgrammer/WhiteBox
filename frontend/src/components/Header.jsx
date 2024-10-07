import React, { useEffect, useState } from "react";
import { Disclosure, DisclosureButton, DisclosurePanel, Menu, MenuButton, MenuItem, MenuItems, } from "@headlessui/react";
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom';
import { Bars3Icon, BellIcon, XMarkIcon } from "@heroicons/react/24/outline";
import CommunityGenralList from './community/CommunityGenralList'
import "../styles/main/main.css"
import useAuthStore from "../store/useAuthStore";

// 이미지
import  logoImsi from '../public/img/logoImsi.svg'
import  profileCar from '../public/img/profileCar.svg'



// navBar 링크 객체화
const tempURL = `http://localhost:3000/`

const navigation = [
    { name: 'AI판단', href: '', current: false },
    { name: '게시판', href:  'community/general', current: false },
    { name: '정보', href: 'information', current: false },

]

function classNames(...classes) {
    return classes.filter(Boolean).join(" ");
}

function Header() {
    const isLogin = !!localStorage.getItem('accessToken')
    const logout = useAuthStore((state) => state.logout)
    const getUser = useAuthStore((state) => state.getUser)
    const navigate = useNavigate();

    const [ user, setUser ] = useState();

    useEffect(() => {
        setUser(getUser());
    }, [getUser]);
    
    const handleLogoClick = () => {
        navigate('/')
    }

    const handleProfileClick = () => {
        navigate(`/auth/profile/${user.nickname}`);
    };

    const handleLogoutClick = () => {
        logout();
        navigate('/');
    };

    const handleLoginClick = () => {
        navigate('/auth/login');
    }

    const handleSignupClick = () => {
        navigate('/auth/sign-up');
    }
    
    return (
        <Disclosure as="nav" className="nav-bar">
        {/* grid 12 cols gutter 20px */}
        <div className="grid grid-cols-12 gap-x-5 border-b-2">
        <div className="col-span-1"></div>
            {/* 로고와 네비게이션 포함 */}
            <div className="relative flex items-center justify-between col-span-10">
            {/* 로고와 네비게이션 컴포넌트 */}
            <div className="flex flex-1 items-left justify-left">
                {/* 로고 */}
                <div className="flex flex-shrink-0 items-center" id="logo">
                <img
                    alt=""
                    src={logoImsi}
                    className="h-10 w-auto cursor-pointer"
                    onClick={ handleLogoClick }
                />
                </div>
                {/* 네비게이션 링크 -> 화면 줄어들면 없어짐 */}
                <div className="flex">
                    {navigation.map((item) => (
                        <p
                            key={item.name}
                            onClick={() => navigate(item.href)} // Use onClick for navigation
                            aria-current={item.current ? "page" : undefined}
                            className={classNames(
                                item.current
                                    ? "bg-gray-900 text-black"
                                    : "text-black hover:bg-[#B5D2FC] hover:text-gray cursor-pointer", // Add cursor-pointer for better UX
                                "text-sm font-medium items-center menu-button place-content-center"
                            )}
                        >
                            <span className="flex justify-center text-xl">{item.name}</span>
                        </p>
                    ))}
                </div>
            </div>
            {/* 프로필 */}
            <div className="flex items-center absolute right-0">
                <Menu as="div" className="relative ml-3">
                <div>
                    <MenuButton className="relative text-sm">
                    <img
                        alt=""
                        src={profileCar}
                        className="h-10 w-10" // 1당 4pixel
                    />
                    </MenuButton>
                </div>
                {/* 드롭다운 메뉴 아이템들 */}
                <MenuItems
                    transition
                    className="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5 transition focus:outline-none data-[closed]:scale-95 data-[closed]:transform data-[closed]:opacity-0 data-[enter]:duration-100 data-[leave]:duration-75 data-[enter]:ease-out data-[leave]:ease-in"
                >
                    {isLogin ? (
                        <>
                            <MenuItem>
                                <p
                                    onClick={handleProfileClick}
                                    className="cursor-pointer block px-4 py-2 text-sm text-gray-700"
                                >
                                    프로필 보기
                                </p>
                            </MenuItem>
                            <MenuItem>
                                <p
                                    onClick={handleLogoutClick}
                                    className="cursor-pointer block px-4 py-2 text-sm text-gray-700"
                                >
                                    로그아웃
                                </p>
                            </MenuItem>
                        </>
                    ) : (
                        <>
                            <MenuItem>
                                <p
                                    onClick={handleLoginClick}
                                    className="block px-4 py-2 text-sm text-gray-700"
                                >
                                    로그인
                                </p>
                            </MenuItem>
                            <MenuItem>
                                <p
                                    onClick={handleSignupClick}
                                    className="block px-4 py-2 text-sm text-gray-700"
                                >
                                    회원가입
                                </p>
                            </MenuItem>
                        </>
                    )}
                </MenuItems>
                </Menu>
            </div>
            </div>
            <div className="col-span-1"></div>
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
